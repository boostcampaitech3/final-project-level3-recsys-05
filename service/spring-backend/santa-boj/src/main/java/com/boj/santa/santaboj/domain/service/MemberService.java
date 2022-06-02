package com.boj.santa.santaboj.domain.service;

import com.boj.santa.santaboj.domain.entity.Member;
import com.boj.santa.santaboj.exceptions.SolvedAcNotFoundException;
import com.boj.santa.santaboj.exceptions.UsernameAlreadyExistException;

public interface MemberService {
    Member registerNewMember(String username, String password, String bojId) throws SolvedAcNotFoundException, UsernameAlreadyExistException;
    Member findUserByUsername(String username);
    Member findMemberByAuthentication();
}
