package com.boj.santa.santaboj.repository;

import com.boj.santa.santaboj.domain.entity.Member;
import com.boj.santa.santaboj.domain.repository.MemberRepository;
import org.assertj.core.api.Assertions;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import javax.transaction.Transactional;

@SpringBootTest
@Transactional
class MemberRepositoryImplTest {

    @Autowired
    MemberRepository memberRepository;

    @Test
    void saveTest(){
        Member member = Member.createMember("abc", "mbc", "abc");
        Member member2 = memberRepository.save(member);
        Member findMember = memberRepository.findByUsername(member2.getUsername());
        Assertions.assertThat(findMember.getUsername()).isEqualTo(member2.getUsername());
    }
}