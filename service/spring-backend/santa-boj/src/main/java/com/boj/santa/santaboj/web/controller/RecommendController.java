package com.boj.santa.santaboj.web.controller;

import com.boj.santa.santaboj.domain.Member;
import com.boj.santa.santaboj.service.MemberService;
import com.boj.santa.santaboj.service.PredictResultDTO;
import com.boj.santa.santaboj.service.PredictResultService;
import com.fasterxml.jackson.core.JsonProcessingException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.net.MalformedURLException;

@Controller
@RequiredArgsConstructor
@Slf4j
public class RecommendController {

    private final PredictResultService predictResultService;
    private final MemberService memberService;

    @GetMapping("/nologin")
    public String nologinResult(@RequestParam String bojId, Model model) throws JsonProcessingException, MalformedURLException {

        PredictResultDTO predictResult = predictResultService.getPredictResult(bojId);
        log.info("predict result by model [{}]", predictResult.getModelType());

        model.addAttribute("bojId", bojId);
        model.addAttribute("predictResult", predictResult);

        return "nologin";
    }

    @GetMapping("/result")
    public String recommendResult(Model model) throws MalformedURLException, JsonProcessingException {
        Member member = memberService.findMemberByAuthentication();
        String username = member.getUsername();

        PredictResultDTO predictResult = predictResultService.getPredictResult(username);
        log.info("predict result by model [{}]", predictResult.getModelType());

        model.addAttribute("username", username);
        model.addAttribute("predictResult", predictResult);

        return "result";
    }
}
