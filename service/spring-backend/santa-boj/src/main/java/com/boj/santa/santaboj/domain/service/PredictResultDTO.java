package com.boj.santa.santaboj.domain.service;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
public class PredictResultDTO {
    @JsonProperty("non_filtering_output")
    private List<String> nonFilteringOutput;
    @JsonProperty("lately_filtering_output")
    private List<String> latelyFilteringOutput;
    @JsonProperty("total_filtering_output")
    private List<String> totalFilteringOutput;
    @JsonProperty("model_type")
    private String modelType;
}
