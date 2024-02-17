FROM nginx:stable

COPY nginx/default.conf.tpl /etc/nginx/default.conf.tpl
COPY nginx/run.sh /scripts/
COPY app/ /app

# Forward request logs to Docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

EXPOSE 80

RUN touch /etc/nginx/conf.d/default.conf && \
    chmod +x /scripts/run.sh

ENV PATH="/scripts:$PATH"

CMD ["nginx", "-g", "daemon off;"]