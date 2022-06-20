package com.boj.santa.santaboj.domain.service;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Getter;
import lombok.Setter;

import java.util.List;
import java.util.Map;

@Getter
@Setter
public class PredictResultDTO {
    @JsonProperty("problems")
    private List<Map<String, String>> problems;
    @JsonProperty("tag")
    private List<String> tag;
}
