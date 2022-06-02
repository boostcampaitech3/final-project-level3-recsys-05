package com.boj.santa.santaboj.web.controller;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
@AllArgsConstructor
public class TotalProblemInfoDTO {
    private String problemId;
    private String problemName;
    private String usedModelName;
}
