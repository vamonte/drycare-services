
FROM vamonte/uwsgi-docker
MAINTAINER vamonte

# Set correct environment variables.
ENV HOME /root


# Use baseimage-docker's init process.
CMD ["/sbin/my_init"]

#Logging
RUN mkdir /var/log/drycare

ADD app/ /home/app/
RUN pip install -r /home/app/requirement.txt

EXPOSE 80

# Enable uWSGI and nginx
RUN rm -f /etc/service/uwsgi/down /etc/service/nginx/down

