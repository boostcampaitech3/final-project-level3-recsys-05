package com.boj.santa.santaboj.domain.service;

import com.fasterxml.jackson.core.JsonProcessingException;

import java.net.MalformedURLException;
import java.util.List;
import java.util.Map;

public interface PredictResultService {
    PredictResultDTO getPredictResult(String bojId) throws MalformedURLException, JsonProcessingException;
    Map<String, String> problemsTitles(List<String> problems) throws JsonProcessingException;
}
