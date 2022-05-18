package com.boj.santa.santaboj.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.assertj.core.api.Assertions;
import org.junit.jupiter.api.Test;

import java.net.MalformedURLException;
import java.util.List;


class PredictResultServiceImplTest {
    PredictResultService predictResultService = new PredictResultServiceImpl("http://101.101.218.250:30005", new ObjectMapper());

    @Test
    public void test1() throws MalformedURLException, JsonProcessingException {
        PredictResultDTO predictResultDTO = predictResultService.getPredictResult("kjpark4321");

        Assertions.assertThat(predictResultDTO.getNonFilteringOutput()).isNotNull();
        Assertions.assertThat(predictResultDTO.getLatelyFilteringOutput()).isNotNull();;
        Assertions.assertThat(predictResultDTO.getTotalFilteringOutput()).isNotNull();;

    }
}