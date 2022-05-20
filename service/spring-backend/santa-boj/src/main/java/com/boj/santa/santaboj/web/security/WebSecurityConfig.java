package com.boj.santa.santaboj.web.security;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

@RequiredArgsConstructor
@EnableWebSecurity
public class WebSecurityConfig {

    private final JwtAuthenticationEntryPoint unauthorizedHandler;
//    private final JwtAuthenticationFilter jwtAuthenticationFilter;

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
                .csrf()
                .disable()
                .httpBasic()
                .disable()
                .logout()
                .logoutSuccessUrl("/login").deleteCookies("Auth-Token")
                .and()
                .authorizeRequests()
                .mvcMatchers("/", "/css/**", "/scripts/**", "/plugin/**", "/fonts/**", "/login")
                .permitAll()
                .and()
                .headers().frameOptions().disable()
                .and()
                .exceptionHandling()
                .authenticationEntryPoint(unauthorizedHandler)
                .and()
                .sessionManagement() //(4)
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
                .and()
                .addFilterBefore(new JwtAuthenticationFilter(), UsernamePasswordAuthenticationFilter.class)
                .authorizeRequests()
                .antMatchers("/result/**", "/logout")
                .hasAnyAuthority("USER");


//                .authorizeRequests()
//                .antMatchers("/signup")
//                .authenticated()
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