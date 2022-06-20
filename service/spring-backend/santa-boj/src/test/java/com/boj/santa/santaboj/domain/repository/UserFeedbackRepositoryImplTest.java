package com.boj.santa.santaboj.domain.repository;

import com.boj.santa.santaboj.domain.entity.Member;
import com.boj.santa.santaboj.domain.entity.UserFeedback;
import com.boj.santa.santaboj.domain.service.MemberService;
import com.boj.santa.santaboj.exceptions.SolvedAcNotFoundException;
import com.boj.santa.santaboj.exceptions.UsernameAlreadyExistException;
import org.aspectj.lang.annotation.Before;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.event.annotation.BeforeTestClass;

import javax.naming.Name;
import javax.transaction.Transactional;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
class UserFeedbackRepositoryImplTest {

    @Autowired
    private UserFeedbackRepository userFeedbackRepository;
    @Autowired
    private MemberService memberService;

    @BeforeEach
    public void setup() throws SolvedAcNotFoundException, UsernameAlreadyExistException {
        memberService.registerNewMember("kjpark4321", "1234", "kjpark4321");
    }

    @Test
    @Transactional
    void getFeedbackCount() {

        Member testMember = memberService.findUserByUsername("kjpark4321");
        UserFeedback userFeedback1 = UserFeedback.createUserFeedback(testMember, "testModel");
        UserFeedback userFeedback2 = UserFeedback.createUserFeedback(testMember, "testModel");
        userFeedbackRepository.saveUserFeedback(userFeedback1);
        userFeedbackRepository.saveUserFeedback(userFeedback2);

        Long count = userFeedbackRepository.getUserFeedbackCount("testModel", testMember);

        org.assertj.core.api.Assertions.assertThat(count).isGreaterThan(0L);

    }

    @Test
    @Transactional
    void getZeroFeedbackCount() {
        Member testMember = memberService.findUserByUsername("kjpark4321");
        Long count = userFeedbackRepository.getUserFeedbackCount("testModel", testMember);
        org.assertj.core.api.Assertions.assertThat(count).isEqualTo(0L);
    }

}