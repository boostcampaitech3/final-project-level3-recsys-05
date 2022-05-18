package com.boj.santa.santaboj.service;

import com.fasterxml.jackson.core.JsonProcessingException;

import java.net.MalformedURLException;

public interface PredictResultService {
    PredictResultDTO getPredictResult(String username) throws MalformedURLException, JsonProcessingException;
}
