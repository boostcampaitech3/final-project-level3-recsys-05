package com.boj.santa.santaboj.domain.service;

import com.boj.santa.santaboj.domain.entity.Member;
import com.boj.santa.santaboj.domain.repository.MemberRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import javax.transaction.Transactional;

@Service
@Slf4j
@RequiredArgsConstructor
public class MemberServiceImpl implements MemberService{

    private final MemberRepository memberRepository;
    private final BCryptPasswordEncoder bCryptPasswordEncoder;

    @Override
    @Transactional
    public Member registerNewMember(String username, String password, String bojId) {

        password = bCryptPasswordEncoder.encode(password);
        Member findMember = memberRepository.findByUsername(username);
        if (findMember != null){
            log.warn("[{}] username has been already used", username);
            return null;
        }
        Member newMember = Member.createMember(username, password, bojId);
        Member result = memberRepository.save(newMember);
        return result;
    }

    @Override
    public Member findUserByUsername(String username) {
        return memberRepository.findByUsername(username);
    }

    @Override
    public Member findMemberByAuthentication() {
        String principal = (String) SecurityContextHolder.getContext().getAuthentication().getPrincipal();

        return findUserByUsername(principal);
    }
}
