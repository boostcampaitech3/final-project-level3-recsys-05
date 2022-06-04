package com.boj.santa.santaboj.web.controller;

import com.boj.santa.santaboj.domain.entity.Member;
import com.boj.santa.santaboj.domain.service.MemberService;
import com.boj.santa.santaboj.web.security.JwtTokenProvider;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@RequiredArgsConstructor
@Controller
public class MainController {

    private final MemberService memberService;

    @GetMapping("/")
    public String index(Model model){


        String principal = (String) SecurityContextHolder.getContext().getAuthentication().getPrincipal();

        model.addAttribute("principal", principal);

        return "index";
    }

    @GetMapping("/newbie")
    public String newbie(Model model){

        Member authMember = memberService.findMemberByAuthentication();
        String principal = (String) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
        model.addAttribute("principal", principal);
        return "newbie";
    }

}
