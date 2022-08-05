#!/bin/bash

ssh janpeterka 'mysqldump kucharka > kucharka_dump.sql'
echo "✅ Production database dumped"

sudo mysql -u root kucharka -e "source /home/jan/programming/kucharka/bin/delete-all-tables.sql"
echo "✅ All tables were deleted"

scp janpeterka:~/kucharka_dump.sql ./
echo "✅ Dump was copied to local machine"

sudo mysql -u root kucharka < ./kucharka_dump.sql
echo "✅ Dump was loaded to database"

rm -f ./kucharka_dump.sql
echo "✅ Dump file was deleted"
