package com.boj.santa.santaboj.domain.repository;

import com.boj.santa.santaboj.domain.entity.Member;

public interface MemberRepository {
    Member save(Member member);
    Member findById(Long id);
    Member findByUsername(String username);
}
