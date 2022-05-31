package com.boj.santa.santaboj.domain.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.exc.MismatchedInputException;
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
public class PredictResultServiceImpl implements PredictResultService{

    private final ObjectMapper objectMapper;
    private final String url;

    public PredictResultServiceImpl(@Value("${model.server}") String url, ObjectMapper objectMapper){
        this.objectMapper = objectMapper;
        this.url = url;
    }


    @Override
    public PredictResultDTO getPredictResult(String username) throws JsonProcessingException {
        HttpHeaders httpHeaders = new HttpHeaders();
        httpHeaders.setContentType(new MediaType("application", "json", StandardCharsets.UTF_8));

        Map<String, Object> map = new HashMap<>();
        map.put("username", username);
        map.put("key", 123456);

        String body = objectMapper.writeValueAsString(map);

        HttpEntity<String> entity = new HttpEntity<>(body, httpHeaders);

        RestTemplate restTemplate = new RestTemplate();
        ResponseEntity<String> responseEntity = restTemplate.exchange(this.url, HttpMethod.POST, entity, String.class);
        PredictResultDTO resultDTO;
        try {
            resultDTO = objectMapper.readValue(responseEntity.getBody(), PredictResultDTO.class);
        } catch (MismatchedInputException e){
            log.error("not found user in boj [{}]", username);
            return null;
        }


        return resultDTO;
    }

    @Override
    public Map<String, String> problemsTitles(List<String> problems) throws JsonProcessingException {

        HttpHeaders httpHeaders = new HttpHeaders();
        httpHeaders.setContentType(new MediaType("application", "json", StandardCharsets.UTF_8));

        StringBuffer problemIds = new StringBuffer("");

        for (String problemId : problems){
            problemIds.append(problemId);
            problemIds.append(',');
        }
        problemIds.deleteCharAt(problemIds.length()-1);


        UriComponentsBuilder builder = UriComponentsBuilder.fromHttpUrl("https://solved.ac/api/v3/problem/lookup")
                .queryParam("problemIds", problemIds.toString());


        HttpEntity<String> entity = new HttpEntity<>(httpHeaders);
        RestTemplate restTemplate = new RestTemplate();
        ResponseEntity<String> responseEntity = restTemplate.exchange(
                builder.toUriString(), HttpMethod.GET, entity, String.class);

        Map[] ProblemInfoDTO = objectMapper.readValue(responseEntity.getBody(), Map[].class);
        HashMap<String, String> problemInfoMap = new HashMap<>();

        for(Map result : ProblemInfoDTO){
            Map<String, Object> real_object = (Map<String, Object>) result;
            Map<String, String> probInfo = new HashMap<>();
            problemInfoMap.put(Integer.toString((Integer)real_object.get("problemId")), (String) real_object.get("titleKo"));
        }
        
        return problemInfoMap;
    }


}
