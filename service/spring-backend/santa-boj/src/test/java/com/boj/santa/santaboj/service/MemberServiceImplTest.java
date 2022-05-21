package com.boj.santa.santaboj.service;

import com.boj.santa.santaboj.domain.Member;
import org.assertj.core.api.Assertions;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.annotation.Rollback;

@SpringBootTest
class MemberServiceImplTest {

    @Autowired
    MemberService memberService;

    @Test
    void registerTest(){
        Member member = memberService.registerNewMember("abc", "hello", "abc");
        Assertions.assertThat(member).isNotNull();
    }

    @Test
    void duplicateRegisterTest(){
        Member member = memberService.registerNewMember("bcd", "hello", "abc");
        Member member2 = memberService.registerNewMember("bcd", "world!", "abc");
        Assertions.assertThat(member).isNotNull();
        Assertions.assertThat(member2).isNull();
    }
}