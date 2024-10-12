postgres -c max_connections=1000 \
            -c shared_buffers=256MB \
            -c effective_cache_size=768MB \
            -c maintenance_work_mem=64MB \
            -c checkpoint_completion_target=0.7 \
            -c wal_buffers=16MB \
            -c default_statistics_target=100;
while !</dev/tcp/db/5432; do sleep 1; done;
psql -U postgres -d kokoc;
CREATE EXTENSION IF NOT EXISTS pg_trgm;