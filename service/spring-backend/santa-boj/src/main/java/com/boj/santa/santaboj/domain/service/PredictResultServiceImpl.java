package com.boj.santa.santaboj.domain.service;

import com.boj.santa.santaboj.domain.entity.Member;
import com.boj.santa.santaboj.domain.entity.UserFeedback;
import com.boj.santa.santaboj.domain.repository.UserFeedbackRepository;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.exc.MismatchedInputException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import java.nio.charset.StandardCharsets;
import java.util.*;

@Service
@Slf4j
public class PredictResultServiceImpl implements PredictResultService {

    private final ObjectMapper objectMapper;
    private final String url;
    private final UserFeedbackRepository userFeedbackRepository;
    private final MemberService memberService;

    @Value("${model.kind}")
    private List<String> modelNames;


    public PredictResultServiceImpl(
            @Value("${model.server}") String url,
            ObjectMapper objectMapper,
            UserFeedbackRepository userFeedbackRepository,
            MemberService memberService
    ) {
        this.objectMapper = objectMapper;
        this.url = url;
        this.userFeedbackRepository = userFeedbackRepository;
        this.memberService = memberService;
    }


    @Override
    public PredictResultDTO getPredictResult(String bojId, boolean isMember, Member member) throws JsonProcessingException {
        HttpHeaders httpHeaders = new HttpHeaders();
        httpHeaders.setContentType(new MediaType("application", "json", StandardCharsets.UTF_8));
        Map<String, Object> map = new HashMap<>();
        Map<String, Map<String, Long>> modelLikedMap = new HashMap<>();

        if (isMember) {
//            Member userByUsername = memberService.findUserByUsername();

            for (String model : modelNames) {
                Map<String, Long> eachModelLikedMap = new HashMap<>();

                Long count = userFeedbackRepository.getUserFeedbackCount(model, member);
                System.out.println("model = " + model);
                System.out.println("count = " + count);
                eachModelLikedMap.put("pos_click", count);
                eachModelLikedMap.put("total_view", member.getTotalView().longValue());
                modelLikedMap.put(model, eachModelLikedMap);
            }

        }
        map.put("model_type_click", modelLikedMap);

        map.put("username", bojId);
        map.put("key", 123456);


        String body = objectMapper.writeValueAsString(map);

        HttpEntity<String> entity = new HttpEntity<>(body, httpHeaders);

        RestTemplate restTemplate = new RestTemplate();
        ResponseEntity<String> responseEntity = restTemplate.exchange(this.url, HttpMethod.POST, entity, String.class);
        PredictResultDTO resultDTO;
        try {
            resultDTO = objectMapper.readValue(responseEntity.getBody(), PredictResultDTO.class);
        } catch (MismatchedInputException e) {
            log.error("not found user in boj [{}]", bojId);
            return null;
        }


        return resultDTO;
    }

    @Override
    public Map<String, String> problemsTitles(List<String> problems) throws JsonProcessingException {

        HttpHeaders httpHeaders = new HttpHeaders();
        httpHeaders.setContentType(new MediaType("application", "json", StandardCharsets.UTF_8));

        StringBuffer problemIds = new StringBuffer("");

        for (String problemId : problems) {
            problemIds.append(problemId);
            problemIds.append(',');
        }
        problemIds.deleteCharAt(problemIds.length() - 1);


        UriComponentsBuilder builder = UriComponentsBuilder.fromHttpUrl("https://solved.ac/api/v3/problem/lookup")
                .queryParam("problemIds", problemIds.toString());


        HttpEntity<String> entity = new HttpEntity<>(httpHeaders);
        RestTemplate restTemplate = new RestTemplate();
        ResponseEntity<String> responseEntity = restTemplate.exchange(
                builder.toUriString(), HttpMethod.GET, entity, String.class);

        Map[] ProblemInfoDTO = objectMapper.readValue(responseEntity.getBody(), Map[].class);
        HashMap<String, String> problemInfoMap = new HashMap<>();

        for (Map result : ProblemInfoDTO) {
            Map<String, Object> real_object = (Map<String, Object>) result;
            Map<String, String> probInfo = new HashMap<>();
            problemInfoMap.put(Integer.toString((Integer) real_object.get("problemId")), (String) real_object.get("titleKo"));
        }


        return problemInfoMap;
    }

    @Override
    public UserFeedback saveFeedback(Member member, String modelName) {

        UserFeedback userFeedback = UserFeedback.createUserFeedback(member, modelName);
        userFeedbackRepository.saveUserFeedback(userFeedback);
        return userFeedback;
    }


}
