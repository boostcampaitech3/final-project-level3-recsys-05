package com.boj.santa.santaboj.web.security;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
public class WebSecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
                .csrf()
                .disable()
                .authorizeRequests()
                .mvcMatchers("/","/css/**","/scripts/**","/plugin/**","/fonts/**")
                .permitAll()
//                .and()
//                .authorizeRequests()
//                .antMatchers("/").permitAll()
//                .sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS)
//                .and()
//                .antMatchers("/login").hasRole("USER")
//                .requestMatchers(CorsUtils::isPreFlightRequest).permitAll()
//                .anyRequest().hasRole("USER")
//                .and()
//                .addFilterBefore(new JwtAuthenticationFilter(jwtTokenProvider, loginStatusManager),
//                        UsernamePasswordAuthenticationFilter.class)
        ;
        return http.build();
    }
}