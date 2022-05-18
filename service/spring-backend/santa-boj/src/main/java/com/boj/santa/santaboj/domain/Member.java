package com.boj.santa.santaboj.domain;

import lombok.Getter;

import javax.persistence.*;

@Entity
@Getter
public class Member {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(unique = true, nullable = false)
    private String username;

    @Column(nullable = false)
    private String password;

    public static Member createMember(String username, String password){
        Member member = new Member();
        member.username = username;
        member.password = password;
        return member;
    }
}
