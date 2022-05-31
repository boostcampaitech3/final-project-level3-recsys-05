package com.boj.santa.santaboj.service;

import com.boj.santa.santaboj.domain.service.PredictResultDTO;
import com.boj.santa.santaboj.domain.service.PredictResultService;
import com.boj.santa.santaboj.domain.service.PredictResultServiceImpl;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.assertj.core.api.Assertions;
import org.junit.jupiter.api.Test;

import java.net.MalformedURLException;


class PredictResultServiceImplTest {
    PredictResultService predictResultService = new PredictResultServiceImpl("http://101.101.218.250:30002/models", new ObjectMapper());

    @Test
    public void test1() throws MalformedURLException, JsonProcessingException {
        PredictResultDTO predictResultDTO = predictResultService.getPredictResult("kjpark4321");

        Assertions.assertThat(predictResultDTO).isNotNull();

    }
}