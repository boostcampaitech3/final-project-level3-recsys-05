package com.boj.santa.santaboj.web.controller;

import com.boj.santa.santaboj.domain.entity.Member;
import com.boj.santa.santaboj.domain.service.MemberService;
import com.boj.santa.santaboj.exceptions.SolvedAcNotFoundException;
import com.boj.santa.santaboj.exceptions.UsernameAlreadyExistException;
import com.boj.santa.santaboj.web.security.JwtTokenProvider;
import com.boj.santa.santaboj.web.security.UserAuthentication;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
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
    private final BCryptPasswordEncoder bCryptPasswordEncoder;

    @GetMapping ("/signup")
    public String signUp(Model model){
        model.addAttribute("already", 'N');

        return "signup";
    }

    @PostMapping ("/signup")
    public String handleSignUp(MemberDTO member, Model model){
        log.info("trying to sign up {}", member.getUsername());
        try {
            Member result = memberService.registerNewMember(member.getUsername(), member.getPassword(), member.getBojId());
        } catch (SolvedAcNotFoundException e) {
            log.error("no solved ac user found");
            return "redirect:signup";
        } catch (UsernameAlreadyExistException e){
            log.error("[{}] username has been already used", member.getBojId());
            model.addAttribute("already", 'Y');
            model.addAttribute("already", 'Y');
            return "redirect:signup";
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
            if (username.equals(userByUsername.getUsername()) && bCryptPasswordEncoder.matches(password, userByUsername.getPassword())) {
                Authentication authentication = new UserAuthentication(username, password, grantedAuthorityList);
                String token = JwtTokenProvider.generateToken(authentication);
                Cookie authToken = new Cookie("Auth-Token", token);
                response.addCookie(authToken);
                log.info("[{}] user sign in", username);
                return "redirect:/";
            }
        }
        return "redirect:/login";
    }
}
