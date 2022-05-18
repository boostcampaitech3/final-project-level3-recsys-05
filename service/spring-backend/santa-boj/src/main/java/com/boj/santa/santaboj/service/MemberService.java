package com.boj.santa.santaboj.service;

import com.boj.santa.santaboj.domain.Member;

public interface MemberService {
    Member registerNewMember(String username, String password);
    Member findUserByUsername(String username);
}
