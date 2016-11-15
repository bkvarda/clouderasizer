#If you want to run it in non-interactive mode, supply these arguments
CM_HOST=$1
CMUSERNAME=$2
CMPASSWORD=$3
FROM=$4
TO=$5


#If no args supplied, read CM-related info from interactive shell
if [ -z $CM_HOST ] || [ -z $CMUSERNAME ] || [ -z $CMPASSWORD ]; then
  read -p "Enter CM hostname/port (IE http://localhost:7180): " CM_HOST
  read -p "Enter Collection start date (IE 2016-01-01T00:00:00 - press enter for 1 year ago) " FROM
  read -p "Enter Collection end date (IE 2016-11-05T:00:00:00  - press enter for today) " TO
  read -p "Enter CM Username: " CMUSERNAME
  read -s -p "Enter CM Password: " CMPASSWORD
  echo ''
fi

#If dates haven't been specified, set end date to current date and start date from a year ago
if [ -z $TO ]; then
  TO="$(date "+%Y-%m-%dT00:00:00")"
fi

YEAR="$(date "+%Y")"

if [ -z $FROM ]; then
  FROMYEAR=$(($YEAR -1))
  FROM="$(date "+$FROMYEAR-%m-%dT00:00:00")"
fi

LOGIN_STRING="$CMUSERNAME:$CMPASSWORD"

#Check that curl exists, if it doesn't this script can't continue
if ! type "curl" > /dev/null; then
  echo "This script requires curl to execute. Install curl before continuing"
  exit 1
fi


#Check that we can even connect to Cloudera Manager and that the endpoints exist
VERSION_ENDPOINT="$CM_HOST/api/version"

TRY_HEADER="$(curl --insecure --silent --silent -i -u $LOGIN_STRING -X GET $VERSION_ENDPOINT)"

if [[ -z "$TRY_HEADER" ]]; then
  echo "Unable to connect to CM. You may have entered an incorrect hostname or port"
  exit 1
elif [[ "$TRY_HEADER" != *"CLOUDERA_MANAGER_SESSIONID"* ]]; then
  echo "The entered hostname/port is not Cloudera Manager. Make sure you're entering the proper host/port"
  exit 1 
fi

CM_API_VERSION="$(curl --insecure --silent --silent -u $LOGIN_STRING -X GET $VERSION_ENDPOINT)"

if [[ "$CM_API_VERSION" == *"Bad credential"* ]]; then
echo "Invalid credentials for CM. Rerun the script with correct credentials"
exit 1
fi


TIMESERIES_ENDPOINT="$CM_HOST/api/$CM_API_VERSION/timeseries/"
METHOD="GET"

#Download a bunch of data

echo "Downloading data from Cloudera Manager..."
echo "Endpoint is: $TIMESERIES_ENDPOINT"
echo "Starting collection from: $FROM"
echo "Collecting until: $TO"

curl --insecure --silent -u $LOGIN_STRING -H "Content-Type: application/json" -X $METHOD "$TIMESERIES_ENDPOINT?query=SELECT+total_append_rate_across_regionservers+WHERE+serviceType+=+HBASE&from=$FROM&to=$TO" -o clouderasizer_hbase_region_appends.json
curl --insecure --silent -u $LOGIN_STRING -H "Content-Type: application/json" -X $METHOD "$TIMESERIES_ENDPOINT?query=SELECT+total_get_rate_across_regionservers+WHERE+serviceType+=+HBASE&from=$FROM&to=$TO" -o clouderasizer_hbase_region_gets.json
curl --insecure --silent -u $LOGIN_STRING -H "Content-Type: application/json" -X $METHOD "$TIMESERIES_ENDPOINT?query=SELECT+total_delete_rate_across_regionservers+WHERE+serviceType+=+HBASE&from=$FROM&to=$TO" -o clouderasizer_hbase_region_deletes.json
curl --insecure --silent -u $LOGIN_STRING -H "Content-Type: application/json" -X $METHOD "$TIMESERIES_ENDPOINT?query=SELECT+total_increment_rate_across_regionservers+WHERE+serviceType+=+HBASE&from=$FROM&to=$TO" -o clouderasizer_hbase_region_increments.json
curl --insecure --silent -u $LOGIN_STRING -H "Content-Type: application/json" -X $METHOD "$TIMESERIES_ENDPOINT?query=SELECT+total_mem_rss_across_regionservers+WHERE+serviceType+=+HBASE&from=$FROM&to=$TO" -o clouderasizer_hbase_rs_memory.json
curl --insecure --silent -u $LOGIN_STRING -H "Content-Type: application/json" -X $METHOD "$TIMESERIES_ENDPOINT?query=SELECT+total_regions_slow_to_respond_across_htables+WHERE+serviceType+=+HBASE&from=$FROM&to=$TO" -o clouderasizer_hbase_tables_slow.json
curl --insecure --silent -u $LOGIN_STRING -H "Content-Type: application/json" -X $METHOD "$TIMESERIES_ENDPOINT?query=SELECT+total_read_requests_rate_across_regionservers+WHERE+serviceType+=+HBASE&from=$FROM&to=$TO" -o clouderasizer_hbase_region_reads.json
curl --insecure --silent -u $LOGIN_STRING -H "Content-Type: application/json" -X $METHOD "$TIMESERIES_ENDPOINT?query=SELECT+total_write_requests_rate_across_regionservers+WHERE+serviceType+=+HBASE&from=$FROM&to=$TO" -o clouderasizer_hbase_region_writes.json
curl --insecure --silent -u $LOGIN_STRING -H "Content-Type: application/json" -X $METHOD "$TIMESERIES_ENDPOINT?query=SELECT+block_cache_express_hit_ratio_across_regionservers+WHERE+serviceType+=+HBASE&from=$FROM&to=$TO" -o clouderasizer_hbase_block_cache_hit.json
curl --insecure --silent -u $LOGIN_STRING -H "Content-Type: application/json" -X $METHOD "$TIMESERIES_ENDPOINT?query=SELECT+total_allocated_vcores_across_yarn_pools+WHERE+serviceType+=+YARN&from=$FROM&to=$TO" -o clouderasizer_yarn_vcores.json
curl --insecure --silent -u $LOGIN_STRING -H "Content-Type: application/json" -X $METHOD "$TIMESERIES_ENDPOINT?query=SELECT+total_allocated_memory_mb_across_yarn_pools+WHERE+serviceType+=+YARN&from=$FROM&to=$TO" -o clouderasizer_yarn_memory.json
curl --insecure --silent -u $LOGIN_STRING -H "Content-Type: application/json" -X $METHOD "$TIMESERIES_ENDPOINT?query=SELECT+total_allocated_containers_across_yarn_pools+WHERE+serviceType+=+YARN&from=$FROM&to=$TO" -o clouderasizer_yarn_containers.json
curl --insecure --silent -u $LOGIN_STRING -H "Content-Type: application/json" -X $METHOD "$TIMESERIES_ENDPOINT?query=SELECT+total_bytes_written_rate_across_datanodes+WHERE+serviceType+=+HDFS&from=$FROM&to=$TO" -o clouderasizer_hdfs_writes.json
curl --insecure --silent -u $LOGIN_STRING -H "Content-Type: application/json" -X $METHOD "$TIMESERIES_ENDPOINT?query=SELECT+total_bytes_read_rate_across_datanodes+WHERE+serviceType+=+HDFS&from=$FROM&to=$TO" -o clouderasizer_hdfs_reads.json
curl --insecure --silent -u $LOGIN_STRING -H "Content-Type: application/json" -X $METHOD "$TIMESERIES_ENDPOINT?query=SELECT+total_dfs_capacity_used_across_datanodes+WHERE+serviceType+=+HDFS&from=$FROM&to=$TO" -o clouderasizer_hdfs_capacity.json
curl --insecure --silent -u $LOGIN_STRING -H "Content-Type: application/json" -X $METHOD "$TIMESERIES_ENDPOINT?query=SELECT+query_duration+FROM+IMPALA_QUERIES&from=$FROM&to=$TO" -o clouderasizer_impala_queries.json
curl --insecure --silent -u $LOGIN_STRING -H "Content-Type: application/json" -X $METHOD "$TIMESERIES_ENDPOINT?query=SELECT+integral(total_num_queries_rate_across_impalads)+WHERE+serviceType+=+IMPALA&from=$FROM&to=$TO" -o clouderasizer_impala_queries_rate.json
curl --insecure --silent -u $LOGIN_STRING -H "Content-Type: application/json" -X $METHOD "$TIMESERIES_ENDPOINT?query=SELECT+total_catalog_num_tables_across_impalads+WHERE+serviceType+=+IMPALA&from=$FROM&to=$TO" -o clouderasizer_impala_num_tables.json
curl --insecure --silent -u $LOGIN_STRING -H "Content-Type: application/json" -X $METHOD "$TIMESERIES_ENDPOINT?query=SELECT+total_mem_pool_total_bytes_across_impalads+WHERE+serviceType+=+IMPALA&from=$FROM&to=$TO" -o clouderasizer_impala_mem_pool.json

#make an output directory
mkdir clouderasizer_output

#copy the files there
cp clouderasizer_*.json clouderasizer_output

echo "Creating zip for data..."

#zip it up
zip -r clouderasizer_output.zip clouderasizer_output

echo "clouderasizer_output.zip created"
echo "Cleaning up temporary files..."
#delete the folder
rm -R clouderasizer_output

#delete the json files
rm clouderasizer_*.json

echo "Done"
