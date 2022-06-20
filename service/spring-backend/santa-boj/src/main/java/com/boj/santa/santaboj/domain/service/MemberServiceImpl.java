package com.boj.santa.santaboj.domain.service;

import com.boj.santa.santaboj.domain.entity.Member;
import com.boj.santa.santaboj.domain.repository.MemberRepository;
import com.boj.santa.santaboj.exceptions.SolvedAcNotFoundException;
import com.boj.santa.santaboj.exceptions.UsernameAlreadyExistException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.*;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import javax.transaction.Transactional;
import java.nio.charset.StandardCharsets;

@Service
@Slf4j
@RequiredArgsConstructor
public class MemberServiceImpl implements MemberService{

    private final MemberRepository memberRepository;
    private final BCryptPasswordEncoder bCryptPasswordEncoder;
    private final String solvedAcUrl = "https://solved.ac/api/v3";

    @Override
    @Transactional
    public Member registerNewMember(String username, String password, String bojId) throws SolvedAcNotFoundException, UsernameAlreadyExistException {

        password = bCryptPasswordEncoder.encode(password);
        Member findMember = memberRepository.findByUsername(username);
        if (findMember != null){
            log.warn("[{}] username has been already used", username);
            throw new UsernameAlreadyExistException("username has been already used");
        }

        HttpHeaders httpHeaders = new HttpHeaders();
        httpHeaders.setContentType(new MediaType("application", "json", StandardCharsets.UTF_8));

        HttpEntity<String> entity = new HttpEntity<>(null, httpHeaders);

        UriComponentsBuilder builder = UriComponentsBuilder.fromHttpUrl(solvedAcUrl + "/user/show")
                .queryParam("handle", bojId);


        RestTemplate restTemplate = new RestTemplate();
        try {
            ResponseEntity<String> responseEntity = restTemplate.exchange(
                    builder.toUriString(), HttpMethod.GET, entity, String.class);
            HttpStatus statusCode = responseEntity.getStatusCode();
        } catch(HttpClientErrorException e){
            log.error("not found solved.ac user [{}]", bojId);
            throw new SolvedAcNotFoundException("solved ac user not found");
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
