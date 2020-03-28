FROM mongo

COPY products.json /products.json

CMD mongoimport \
    --host mongo \
    --db ecommerce \
    --collection products \
    --type json \
    --file /products.json \
    --jsonArray \
    --drop