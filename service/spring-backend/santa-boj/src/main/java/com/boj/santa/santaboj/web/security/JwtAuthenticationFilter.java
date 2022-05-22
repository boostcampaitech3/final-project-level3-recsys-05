package com.boj.santa.santaboj.web.security;

import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.web.filter.OncePerRequestFilter;

import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@Slf4j
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    private Cookie getJwtFromRequest(HttpServletRequest request) {
//        request Header 에서 토큰 가져오는 부분
//        String token = request.getHeader("X-Auth-Token");

        Cookie[] cookies = request.getCookies();
        Cookie token = null;
        if (cookies != null) {
            for (Cookie c : cookies) {
                if (c.getName().equals("Auth-Token")) {
                    token = c;
                }
            }
        }

        return token;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException, IOException {

            try {
                String jwt = getJwtFromRequest(request).getValue(); //request 에서 jwt 토큰을 꺼낸다.
                if (StringUtils.isNotEmpty(jwt) && JwtTokenProvider.validateToken(jwt)) {
                    String userId = JwtTokenProvider.getUserIdFromJWT(jwt); //jwt 에서 사용자 id를 꺼낸다.

                    // Role setting
                    GrantedAuthority grantedAuthority = new SimpleGrantedAuthority("USER");
                    List<GrantedAuthority> grantedAuthorityList = new ArrayList<>();
                    grantedAuthorityList.add(grantedAuthority);

                    UserAuthentication authentication = new UserAuthentication(userId, null, grantedAuthorityList); //id를 인증한다.
                    authentication.setDetails(new WebAuthenticationDetailsSource().buildDetails(request)); //기본적으로 제공한 details 세팅

                    SecurityContextHolder.getContext().setAuthentication(authentication); //세션에서 계속 사용하기 위해 securityContext에 Authentication 등록
                } else {
                    if (StringUtils.isEmpty(jwt)) {
                        log.info("no authorization key");
                        request.setAttribute("unauthorization", "401 인증키 없음.");
                    }

                    if (JwtTokenProvider.validateToken(jwt)) {
                        request.setAttribute("unauthorization", "401-001 인증키 만료.");
                    }
                }
            }   catch (NullPointerException e){
                    log.info("no authorization Token {}", request.getRequestURI());
                }
                catch (Exception ex) {
                    logger.error("Could not set user authentication in security context", ex);
                }
        filterChain.doFilter(request, response);
    }
}
