package com.boj.santa.santaboj.service;

import com.fasterxml.jackson.core.JsonProcessingException;

import java.net.MalformedURLException;

public interface PredictResultService {
    PredictResultDTO getPredictResult(String bojId) throws MalformedURLException, JsonProcessingException;
}
