package com.boj.santa.santaboj.web.controller;

import com.boj.santa.santaboj.domain.entity.Member;
import com.boj.santa.santaboj.domain.service.MemberService;
import com.boj.santa.santaboj.domain.service.PredictResultDTO;
import com.boj.santa.santaboj.domain.service.PredictResultService;
import com.boj.santa.santaboj.domain.service.ProblemInfoDTO;
import com.fasterxml.jackson.core.JsonProcessingException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.net.MalformedURLException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Controller
@RequiredArgsConstructor
@Slf4j
public class RecommendController {

    private final PredictResultService predictResultService;
    private final MemberService memberService;

    @GetMapping("/nologin")
    public String nologinResult(@RequestParam String bojId, Model model) throws JsonProcessingException, MalformedURLException {

        PredictResultDTO predictResult = predictResultService.getPredictResult(bojId);

        List<String> problemIdList = new ArrayList<>();

        for (Map<String, String> obj : predictResult.getProblems()) {
            problemIdList.add(obj.get("output"));
        }

        Map<String, String> problemInfoMap = predictResultService.problemsTitles(problemIdList);

        List<TotalProblemInfoDTO> totalProblemInfoDTOList = new ArrayList<>();
        for(Map<String, String> probInfo : predictResult.getProblems()){
            TotalProblemInfoDTO totalProblemInfoDTO = new TotalProblemInfoDTO(probInfo.get("output"), problemInfoMap.get(probInfo.get("output")), probInfo.get("model_type"));
            totalProblemInfoDTOList.add(totalProblemInfoDTO);
        }

        model.addAttribute("bojId", bojId);
        model.addAttribute("mostCategory", predictResult.getTag());
        model.addAttribute("predictResult", totalProblemInfoDTOList);
        String principal = (String) SecurityContextHolder.getContext().getAuthentication().getPrincipal();

        model.addAttribute("principal", principal);

        return "nologin";
    }

    @GetMapping("/result")
    public String recommendResult(Model model) throws MalformedURLException, JsonProcessingException {
        Member member = memberService.findMemberByAuthentication();
        String username = member.getUsername();

        PredictResultDTO predictResult = predictResultService.getPredictResult(username);
//        log.info("predict result by model [{}]", predictResult.getModelType());
        model.addAttribute("username", username);
        model.addAttribute("predictResult", predictResult);

        return "result";
    }
}
