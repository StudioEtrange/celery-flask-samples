#!/bin/bash
_CURRENT_FILE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
_CURRENT_RUNNING_DIR="$( cd "$( dirname "." )" && pwd )"
. $_CURRENT_FILE_DIR/stella-link.sh include

CONDA_ENV_NAME=$STELLA_APP_NAME
FLASK_APP_NAME=$STELLA_APP_NAME
DEFAULT_REDIS_PORT=6379
DEFAULT_REDIS_DATABASE=0
DEFAULT_REDIS_INSTANCE=auto
DEFAULT_FRONT_PORT=8080

usage() {
	echo "USAGE :"
	echo "----------------"
	echo "o-- general management :"
	echo "L     install <id-sample> : deploy a sample"
	echo "o"
	echo "L     start-front <id-sample> [--port=<port>] [--redis=auto[:<port>]|docker[:<port>]|<host[:port]>] : start flask frontend. --port is the frontend port, default is $DEFAULT_FRONT_PORT. --redis is the instance used, default is $DEFAULT_REDIS_INSTANCE"
	echo "L     stop-front <id-sample> : stop flask frontend."
	echo "o"
	echo "L     start-back <id-sample> [--redis=auto[:<port>]|docker[:<port>]|<host[:port]>] : start celery backend. --redis is the instance used, default is $DEFAULT_REDIS_INSTANCE"
	echo "L     stop-back <id-sample> : stop celery backend."
	echo "o-- celery monitoring :"
	echo "L     start-flower <id-sample> [--port=<port>] : start Flower web ui for monitoring celery. --port is Flower port, default is $DEFAULT_FRONT_PORT"
	echo "L     stop-flower <id-sample>"
	echo "o-- redis management :"
	echo "L     install redis [--redis=auto|docker] : install an 'auto' or 'docker' redis instance. Default redis instance is $DEFAULT_REDIS_INSTANCE"
	echo "L     start redis [--redis=auto[:<port>]|docker[:<port>]] : start an 'auto' or 'docker' redis instance. Default port is $DEFAULT_REDIS_PORT"
	echo "L     stop redis [--redis=auto[:<port>]|docker] : stop an 'auto' or 'docker' redis instance. Default port is $DEFAULT_REDIS_PORT"
}

# COMMAND LINE -----------------------------------------------------------------------------------
PARAMETERS="
ACTION=											'action' 			a				'install start stop start-front start-back stop-front stop-back start-flower stop-flower'
ID=											'id' 			a				'redis sample1 sample2'
"
OPTIONS="
FORCE=''				   'f'		  ''					b			0		'1'					  Force.
REDIS='$DEFAULT_REDIS_INSTANCE' 						'r' 			'string'				s 			0			''		  a redis instance. '<host[:port]>' or 'auto[:<port>]' or 'docker[:<port>]'.
PORT='$DEFAULT_FRONT_PORT' 						'' 			'string'				s 			0			''		  front for frontend api and celery UI listening port.
"
$STELLA_API argparse "$0" "$OPTIONS" "$PARAMETERS" "$STELLA_APP_NAME" "$(usage)" "APPARG" "$@"

#-------------------------------------------------------------------------------------------
# COMPUTE PARAMS

# redis instance
$STELLA_API uri_parse $REDIS
REDIS_HOST=$__stella_uri_host
REDIS_PORT=$__stella_uri_port
REDIS_INSTANCE=$__stella_uri_host
[ "$REDIS_PORT" = "" ] && REDIS_PORT=$DEFAULT_REDIS_PORT
case $REDIS_HOST in
	docker )
			echo "* Using docker redis"
			docker pull redis

			if [ ! "$DOCKER_MACHINE_NAME" = "" ]; then
				REDIS_HOST="$(docker-machine ip $DOCKER_MACHINE_NAME)"
				echo "* with docker-machine $DOCKER_MACHINE_NAME $REDIS_HOST"
			else
				REDIS_HOST=localhost
			fi
		;;
	auto )
			echo "* Using auto deployed redis"
			REDIS_HOST=localhost
		;;
	* )
			echo "* Using already deployed redis"
		;;
esac

# sample
case $ID in
	sample1 )
		SAMPLE_ID=1
		;;
	sample2 )
		SAMPLE_ID=2
		;;
	* )
		;;
esac

SAMPLE_PATH="$STELLA_APP_ROOT/$ID"
REDIS_DATABASE=${SAMPLE_ID}
CONDA_ENV_NAME=${CONDA_ENV_NAME}-${SAMPLE_ID}
FLASK_APP_NAME=${FLASK_APP_NAME}-${SAMPLE_ID}
FLOWER_PORT="$PORT"

# var used in python env
export CELERY_BROKER_URL="redis://$REDIS_HOST:$REDIS_PORT/$REDIS_DATABASE"
export CELERY_RESULT_BACKEND="redis://$REDIS_HOST:$REDIS_PORT/$REDIS_DATABASE"
#export CELERY_RESULT_BACKEND="db+sqlite:///results.sqlite"
export FRONTEND_PORT="$PORT"
export FLASK_APP_NAME="$FLASK_APP_NAME"

# --------------- INSTALL ----------------------------
if [ "$ACTION" = "install" ]; then

	if [ "$ID" = "redis" ]; then
			echo "** Install redis $REDIS_INSTANCE"
			case $REDIS_INSTANCE in
				docker )
						docker pull redis
					;;
				auto )
						$STELLA_API get_feature redis
					;;
				* )
					;;
			esac
	else
		echo "** Install sample $ID"
		$STELLA_API get_feature miniconda

		# create python conda env
		conda create -y -n $CONDA_ENV_NAME python=3.6
		# activation env
		set -h
		source activate $CONDA_ENV_NAME
		# install python dependencies
		pip install -r $SAMPLE_PATH/requirements.txt

		source deactivate $CONDA_ENV_NAME
		set +h
	fi
fi

# --------------- START ----------------------------
if [ "$ACTION" = "start-front" ]; then
	echo "** Start frontend"
	cd "$STELLA_APP_ROOT"

	set -h
	source activate $CONDA_ENV_NAME

	# launch API server
	export PYTHONPATH=.:$PYTHONPATH
	python $SAMPLE_PATH/front.py

	source deactivate $CONDA_ENV_NAME
	set +h
fi

if [ "$ACTION" = "start-back" ]; then
	echo "** Start backend"
	cd "$STELLA_APP_ROOT"

	set -h
	source activate $CONDA_ENV_NAME

	# launch celery
	celery -A ${ID}.back.backapp worker --loglevel=info

	source deactivate $CONDA_ENV_NAME
	set +h
fi

if [ "$ACTION" = "start-flower" ]; then
	echo "** Start Flower UI"
	cd "$STELLA_APP_ROOT"

	set -h
	source activate $CONDA_ENV_NAME

	# launch celery flower UI
	celery -A ${ID}.back.backapp flower --port=$FLOWER_PORT --logging=none

	source deactivate $CONDA_ENV_NAME
	set +h
fi

if [ "$ACTION" = "start" ]; then

	if [ "$ID" = "redis" ]; then
		echo "** Start redis $REDIS_INSTANCE"
		case $REDIS_INSTANCE in
			docker )
					docker run -d -p $REDIS_PORT:6379 --name id-redis redis
				;;
			auto )
					redis-server --port $REDIS_PORT
					#$STELLA_API feature_info redis REDIS
					#export REDIS_HOME=$REDIS_FEAT_INSTALL_ROOT
					#nohup -- $REDIS_HOME/redis-server --port $REDIS_PORT 1>/dev/null 2>&1 &
				;;
			* )
				;;
		esac
	fi

fi

# --------------- STOP ----------------------------
if [ "$ACTION" = "stop-front" ]; then
	echo " ** Stop front"

	# stop api
	kill $(ps aux | grep "$SAMPLE_PATH/front.py" | tr -s " " | cut -d" " -f 2)
fi

if [ "$ACTION" = "stop-back" ]; then
	echo " ** Stop back"
	cd "$STELLA_APP_ROOT"

	set -h
	source activate $CONDA_ENV_NAME

	# stop celery
	celery -A ${ID}.back.backapp control shutdown

	source deactivate $CONDA_ENV_NAME
	set +h
fi

if [ "$ACTION" = "stop-flower" ]; then
	echo " ** Stop Flower UI"
	cd "$STELLA_APP_ROOT"

	set -h
	source activate $CONDA_ENV_NAME

	# stop flower
	kill $(ps aux | grep "celery -A ${ID}.back.backapp flower" | tr -s " " | cut -d" " -f 2)

	source deactivate $CONDA_ENV_NAME
	set +h
fi

if [ "$ACTION" = "stop" ]; then
	if [ "$ID" = "redis" ]; then
		echo " ** Stop redis $REDIS_INSTANCE"

		# stop redis
		case $REDIS_INSTANCE in
			docker )
				docker stop id-redis
				;;
			auto )
				redis-cli -p $REDIS_PORT shutdown
				;;
			* )
				;;
		esac
	fi
fi
