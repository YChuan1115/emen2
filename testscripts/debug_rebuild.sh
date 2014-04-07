python -m emen2.db.create --debug --rootpw=asdf1234

python -m emen2.db.load --debug \
    ~/Dropbox/src/emen2/emen2/db/base.json \
    ~/Dropbox/src/emen2/emen2/exts/em/json/em.json \
    ~/Dropbox/src/ext_ncmi/json/ncmi.json

python -m emen2.db.load --debug \
    --set validation.allow_invalid_email \
    ~/data/import/json/user.json \
    ~/data/import/json/group.json 

python -m emen2.db.load --debug \
    --set validation.allow_invalid_email \
    --set validation.allow_invalid_choice=True \
    --set validation.allow_invalid_reference=True \
    --set record.sequence=False \
    --update_record_max \
    --keytype=record \
    ~/data/import/json/record.json
