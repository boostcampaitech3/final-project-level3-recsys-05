package com.boj.santa.santaboj.web.controller;

import com.boj.santa.santaboj.web.security.JwtTokenProvider;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@RequiredArgsConstructor
@Controller
public class MainController {

    @GetMapping("/")
    public String index(Model model){


        String principal = (String) SecurityContextHolder.getContext().getAuthentication().getPrincipal();

        model.addAttribute("principal", principal);

        return "index";
    }

}
