package com.rrrkren.InsertTimestamp;

import org.apache.kafka.connect.connector.ConnectRecord;
import org.apache.kafka.connect.transforms.Transformation;
import org.apache.kafka.common.cache.Cache;
import org.apache.kafka.common.cache.LRUCache;
import org.apache.kafka.common.cache.SynchronizedCache;
import org.apache.kafka.common.config.ConfigDef;
import org.apache.kafka.connect.connector.ConnectRecord;
import org.apache.kafka.connect.data.Field;
import org.apache.kafka.connect.data.Schema;
import org.apache.kafka.connect.data.SchemaBuilder;
import org.apache.kafka.connect.data.Struct;
import com.fasterxml.jackson.databind.ObjectMapper;

import org.apache.kafka.connect.transforms.util.SchemaUtil;
import org.apache.kafka.connect.transforms.util.SimpleConfig;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

public class InsertTimestamp<S extends ConnectRecord<S>> implements Transformation<S> {
    private final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public S apply(S record) {
        long timestamp = System.currentTimeMillis();

        Map<String, Object> updatedValue = new HashMap<String, Object>();

        if (record.value() instanceof Map) {
            updatedValue.putAll((Map<String, Object>) record.value());
        }

        updatedValue.put("timestamp", timestamp);

        String updatedValueJson;
        try {
            updatedValueJson = objectMapper.writeValueAsString(updatedValue);
        } catch (Exception e) {
            throw new RuntimeException("Failed to serialize updated value to JSON", e);
        }

        return record.newRecord(
            record.topic(),
            record.kafkaPartition(),
            record.keySchema(),
            record.key(),
            Schema.STRING_SCHEMA,
            updatedValueJson,
            record.timestamp()
        );
    }

    @Override
    public ConfigDef config() {
        return new ConfigDef();
    }

    @Override
    public void close() {
        // Nothing to do on close
    }

    @Override
    public void configure(Map<String, ?> configs) {
        // Configure the SMT if necessary
    }
}