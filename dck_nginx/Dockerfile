FROM nginx:1.11.8
COPY nginx.conf /etc/nginx/nginx.conf
COPY ng-entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
VOLUME /data
EXPOSE 80
CMD ["start"]