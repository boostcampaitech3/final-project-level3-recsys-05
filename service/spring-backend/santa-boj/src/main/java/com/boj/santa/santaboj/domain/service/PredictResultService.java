package com.boj.santa.santaboj.domain.service;

import com.boj.santa.santaboj.domain.entity.Member;
import com.boj.santa.santaboj.domain.entity.UserFeedback;
import com.fasterxml.jackson.core.JsonProcessingException;

import java.net.MalformedURLException;
import java.util.List;
import java.util.Map;

public interface PredictResultService {
    PredictResultDTO getPredictResult(String bojId, boolean isMember, Member member) throws MalformedURLException, JsonProcessingException;
    Map<String, String> problemsTitles(List<String> problems) throws JsonProcessingException;
    UserFeedback saveFeedback(Member member, String modelName);
}
