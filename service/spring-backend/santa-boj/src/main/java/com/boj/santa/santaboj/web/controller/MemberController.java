package com.boj.santa.santaboj.web.controller;

import com.boj.santa.santaboj.domain.Member;
import com.boj.santa.santaboj.service.MemberService;
import com.boj.santa.santaboj.web.security.JwtTokenProvider;
import com.boj.santa.santaboj.web.security.UserAuthentication;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseBody;

import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.ArrayList;
import java.util.List;

@Slf4j
@RequiredArgsConstructor
@Controller
public class MemberController {

    private final MemberService memberService;

    @GetMapping ("/signup")
    public String signUp(Model model){
        model.addAttribute("already", 'N');

        return "signup";
    }

    @PostMapping ("/signup")
    public String handleSignUp(MemberDTO member, Model model){
        log.info("new member sign up {}", member.getUsername());
        Member result = memberService.registerNewMember(member.getUsername(), member.getPassword());
        if (result == null){
            model.addAttribute("already", 'Y');
            log.warn("already username {} exists", member.getUsername());
            model.addAttribute("already", 'Y');
            return "signup";
        }
        log.info("{} member sign up successfully", member.getUsername());
        model.addAttribute("already", 'N');
        return "redirect:/";
    }

    @GetMapping("/login")
    public String login(HttpServletRequest request){
        return "login";
    }

    @PostMapping("/login")
    public String handleLogin(HttpServletResponse response, String username, String password){
        GrantedAuthority grantedAuthority = new SimpleGrantedAuthority("USER");
        List<GrantedAuthority> grantedAuthorityList = new ArrayList<>();
        grantedAuthorityList.add(grantedAuthority);

        Member userByUsername = memberService.findUserByUsername(username);
        if (userByUsername != null) {
            if (username.equals(userByUsername.getUsername()) && password.equals(userByUsername.getPassword())) {
                Authentication authentication = new UserAuthentication(username, password, grantedAuthorityList);
                String token = JwtTokenProvider.generateToken(authentication);
                Cookie authToken = new Cookie("Auth-Token", token);
                response.addCookie(authToken);
                log.info("[{}] user sign in", username);
                return "redirect:/";
            }
        }
        return "redirect:/";
    }

    @GetMapping("/result")
    public String result(){
        return "result";
    }
}
