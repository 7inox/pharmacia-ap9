package pe.edu.upeu.Practica.config;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.cache.autoconfigure.RedisCacheManagerBuilderCustomizer;
import org.springframework.cache.Cache;
import org.springframework.cache.annotation.CachingConfigurer;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.cache.interceptor.CacheErrorHandler;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.Ordered;

@Configuration
@EnableCaching(order = Ordered.LOWEST_PRECEDENCE - 1)
public class CacheConfig implements CachingConfigurer {
    private static final Logger LOG = LoggerFactory.getLogger(CacheConfig.class);

    @Bean
    RedisCacheManagerBuilderCustomizer transactionAwareCache() {
        return builder -> builder.transactionAware();
    }

    @Override
    public CacheErrorHandler errorHandler() {
        return new CacheErrorHandler() {
            @Override
            public void handleCacheGetError(RuntimeException error, Cache cache, Object key) {
                warn(cache, "leer", error);
            }

            @Override
            public void handleCachePutError(RuntimeException error, Cache cache, Object key, Object value) {
                warn(cache, "guardar", error);
            }

            @Override
            public void handleCacheEvictError(RuntimeException error, Cache cache, Object key) {
                warn(cache, "invalidar", error);
            }

            @Override
            public void handleCacheClearError(RuntimeException error, Cache cache) {
                warn(cache, "limpiar", error);
            }

            private void warn(Cache cache, String operation, RuntimeException error) {
                LOG.warn("Caché {}: no se pudo {} ({})", cache.getName(), operation,
                    error.getClass().getSimpleName());
            }
        };
    }
}
