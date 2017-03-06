FROM debian:jessie

#If running on raspberry pi:
#FROM armhf/debian:jessie

MAINTAINER Alexander Machhaus

RUN rm /bin/sh && ln -s /bin/bash /bin/sh # No sh, we want bash.

RUN apt-get update && apt-get install -y \
	python3-pip\
	apache2\
	libapache2-mod-wsgi-py3\
	python3.4\
	python3.4-dev\
	build-essential\
	libpq-dev\
	libjpeg-dev\
	python-imaging\
	libfreetype6\
	libfreetype6-dev\
	libglib2.0-0\
	vim
	

#Setup django traillog virtual environment.
RUN pip3 install virtualenv
RUN virtualenv /virtualenv

ADD camera /var/www/camera
ADD requirements.txt /requirements.txt
RUN source /virtualenv/bin/activate && pip3 install -r /requirements.txt
RUN chown -R www-data:www-data /var/www

# Apache2 vhost definition and mod-wsgi configuration.
ADD 000-default.conf /etc/apache2/sites-available/000-default.conf

#Startup of apache and postgres go here.
ADD run_services.sh /

# New entrypoint, this script calls the script that was the entrypoint for the parent container to do the postgres stuff.
ENTRYPOINT ["/run_services.sh"]

# Port 80should be accessible via network. 
EXPOSE 80


# ENTRYPOINT and CMD commands are inherited from postgres base image, but we override them here!

