{
    "topic_name": $topic_name,
    "partitions_count": 12,
    "replication_factor": 1,
    "configs": [
        {
            "name": "confluent.value.schema.validation",
            "value": $confluent_value_schema_validation
        }
    ]
}
