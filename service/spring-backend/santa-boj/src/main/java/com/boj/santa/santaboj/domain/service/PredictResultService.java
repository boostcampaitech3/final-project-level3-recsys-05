package com.boj.santa.santaboj.domain.service;

import com.fasterxml.jackson.core.JsonProcessingException;

import java.net.MalformedURLException;
import java.util.List;

public interface PredictResultService {
    PredictResultDTO getPredictResult(String bojId) throws MalformedURLException, JsonProcessingException;
    List<String> problemsTitles(List<String> problems);
}
