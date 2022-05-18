package com.boj.santa.santaboj.service;

import com.boj.santa.santaboj.domain.Member;
import com.boj.santa.santaboj.repository.MemberRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import javax.transaction.Transactional;

@Service
@Slf4j
@RequiredArgsConstructor
public class MemberServiceImpl implements MemberService{

    private final MemberRepository memberRepository;

    @Override
    @Transactional
    public Member registerNewMember(String username, String password) {
        Member findMember = memberRepository.findByUsername(username);
        if (findMember != null){
            log.warn("[{}] username has been already used", username);
            return null;
        }
        Member newMember = Member.createMember(username, password);
        Member result = memberRepository.save(newMember);
        return result;
    }

    @Override
    public Member findUserByUsername(String username) {
        return memberRepository.findByUsername(username);
    }
}
