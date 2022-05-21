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

    @Column(nullable = false)
    private String bojId;

    public static Member createMember(String username, String password, String bojId){
        Member member = new Member();
        member.username = username;
        member.password = password;
        member.bojId = bojId;
        return member;
    }
}
