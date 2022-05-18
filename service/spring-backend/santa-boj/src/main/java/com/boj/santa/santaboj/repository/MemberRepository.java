package com.boj.santa.santaboj.repository;

import com.boj.santa.santaboj.domain.Member;

public interface MemberRepository {
    Member save(Member member);
    Member findById(Long id);
    Member findByUsername(String username);
}
