package com.boj.santa.santaboj.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.exc.MismatchedInputException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;

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

        try {
            PredictResultDTO resultDTO = objectMapper.readValue(responseEntity.getBody(), PredictResultDTO.class);
        } catch (MismatchedInputException e){
            log.error("not found user in boj [{}]", username);
        }

        return objectMapper.readValue(responseEntity.getBody(), PredictResultDTO.class);
    }
}
