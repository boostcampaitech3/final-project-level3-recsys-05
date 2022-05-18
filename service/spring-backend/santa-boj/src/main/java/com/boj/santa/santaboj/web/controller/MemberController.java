package com.boj.santa.santaboj.web.controller;

import com.boj.santa.santaboj.domain.Member;
import com.boj.santa.santaboj.service.MemberService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;

@Slf4j
@RequiredArgsConstructor
@Controller
public class MemberController {

    private final MemberService memberService;

    @GetMapping ("/signup")
    public String signUp(){
        return "signup";
    }

    @PostMapping ("/signup")
    public String handleSignUp(MemberDTO member, Model model){
        log.info("new member sign up {}", member.getUsername());
        Member result = memberService.registerNewMember(member.getUsername(), member.getPassword());
        if (result == null){
            model.addAttribute("already", true);
            log.warn("already username {} exists", member.getUsername());
        }
        log.info("{} member sign up successfully", member.getUsername());
        return "redirect:/";
    }
}
