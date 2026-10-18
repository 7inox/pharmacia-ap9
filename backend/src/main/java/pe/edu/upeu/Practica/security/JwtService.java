package pe.edu.upeu.Practica.security;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.io.Decoders;
import io.jsonwebtoken.security.Keys;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.Date;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.nio.charset.StandardCharsets;
import java.util.Base64;
import javax.crypto.SecretKey;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Service;

@Service
public class JwtService {
    private final SecretKey key;
    private final long expirationMinutes;
    public JwtService(@Value("${app.jwt.secret}") String secret, @Value("${app.jwt.expiracion-minutos:60}") long minutes) {
        this.key = Keys.hmacShaKeyFor(Decoders.BASE64.decode(secret));
        this.expirationMinutes = minutes;
    }
    public String generate(UserDetails user, String passwordHash) {
        Instant now = Instant.now();
        return Jwts.builder().subject(user.getUsername())
            .claim("authorities", user.getAuthorities().stream().map(GrantedAuthority::getAuthority).toList())
            .claim("credential", fingerprint(passwordHash))
            .issuedAt(Date.from(now)).expiration(Date.from(now.plus(expirationMinutes, ChronoUnit.MINUTES)))
            .signWith(key).compact();
    }
    public Claims claims(String token) {
        return Jwts.parser().verifyWith(key).build().parseSignedClaims(token).getPayload();
    }
    public boolean currentCredential(Claims claims, UserDetails user) {
        String recorded=claims.get("credential",String.class);
        return recorded!=null && MessageDigest.isEqual(recorded.getBytes(StandardCharsets.US_ASCII),
            fingerprint(user.getPassword()).getBytes(StandardCharsets.US_ASCII));
    }
    private String fingerprint(String hash) {
        try {
            return Base64.getUrlEncoder().withoutPadding().encodeToString(
                MessageDigest.getInstance("SHA-256").digest(hash.getBytes(StandardCharsets.UTF_8)));
        } catch (NoSuchAlgorithmException ex) { throw new IllegalStateException(ex); }
    }
    public long expirationSeconds() { return expirationMinutes * 60; }
}
