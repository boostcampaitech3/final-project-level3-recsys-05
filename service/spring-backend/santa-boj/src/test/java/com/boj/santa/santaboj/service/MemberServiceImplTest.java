package com.boj.santa.santaboj.service;

import com.boj.santa.santaboj.domain.entity.Member;
import com.boj.santa.santaboj.domain.service.MemberService;
import com.boj.santa.santaboj.exceptions.SolvedAcNotFoundException;
import com.boj.santa.santaboj.exceptions.UsernameAlreadyExistException;
import org.assertj.core.api.Assertions;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class MemberServiceImplTest {

    @Autowired
    MemberService memberService;

    @Test
    void registerTest() throws SolvedAcNotFoundException, UsernameAlreadyExistException {
        Member member = memberService.registerNewMember("abc", "hello", "abc");
        Assertions.assertThat(member).isNotNull();
    }

    @Test
    void duplicateRegisterTest() throws SolvedAcNotFoundException, UsernameAlreadyExistException {
        Member member = memberService.registerNewMember("bcd", "hello", "abc");
        Member member2 = memberService.registerNewMember("bcd", "world!", "abc");
        Assertions.assertThat(member).isNotNull();
        Assertions.assertThat(member2).isNull();
    }
}