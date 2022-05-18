package com.boj.santa.santaboj.web.controller;

import com.boj.santa.santaboj.service.PredictResultDTO;
import com.boj.santa.santaboj.service.PredictResultService;
import com.fasterxml.jackson.core.JsonProcessingException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.net.MalformedURLException;

@Controller
@RequiredArgsConstructor
@RequestMapping("/nologin")
@Slf4j
public class NoLoginController {

    private final PredictResultService predictResultService;

    @GetMapping
    public String nologinResult(@RequestParam String username, Model model) throws JsonProcessingException, MalformedURLException {

        PredictResultDTO predictResult = predictResultService.getPredictResult(username);

        model.addAttribute("username", username);
        model.addAttribute("predictResult", predictResult);

        return "nologin";
    }
}
