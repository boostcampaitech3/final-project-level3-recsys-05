package com.boj.santa.santaboj.service;

import com.boj.santa.santaboj.domain.Member;

public interface MemberService {
    Member registerNewMember(String username, String password, String bojId);
    Member findUserByUsername(String username);
    Member findMemberByAuthentication();
}
