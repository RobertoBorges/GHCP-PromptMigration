# Java Testing Patterns

Load these examples only for a Java target. Check library versions against the selected JDK and Spring Boot versions before using them.

## Java Testing Patterns (JUnit 5)

### Project Setup (pom.xml)

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.mockito</groupId>
        <artifactId>mockito-junit-jupiter</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.assertj</groupId>
        <artifactId>assertj-core</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>com.h2database</groupId>
        <artifactId>h2</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

### Service Layer Test

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserService userService;

    @Test
    @DisplayName("Should return user when valid ID provided")
    void findById_WithValidId_ReturnsUser() {
        // Given
        User expectedUser = new User(1L, "John Doe", "john@example.com");
        when(userRepository.findById(1L)).thenReturn(Optional.of(expectedUser));

        // When
        Optional<User> result = userService.findById(1L);

        // Then
        assertThat(result)
            .isPresent()
            .hasValueSatisfying(user -> {
                assertThat(user.getName()).isEqualTo("John Doe");
                assertThat(user.getEmail()).isEqualTo("john@example.com");
            });
    }

    @Test
    @DisplayName("Should return empty when user not found")
    void findById_WithNonExistingId_ReturnsEmpty() {
        // Given
        when(userRepository.findById(anyLong())).thenReturn(Optional.empty());

        // When
        Optional<User> result = userService.findById(999L);

        // Then
        assertThat(result).isEmpty();
    }

    @ParameterizedTest
    @NullAndEmptySource
    @ValueSource(strings = {" ", "   "})
    @DisplayName("Should throw exception for invalid name")
    void create_WithInvalidName_ThrowsException(String invalidName) {
        // Given
        CreateUserDto dto = new CreateUserDto(invalidName, "test@example.com");

        // When/Then
        assertThatThrownBy(() -> userService.create(dto))
            .isInstanceOf(IllegalArgumentException.class)
            .hasMessageContaining("name");
    }
}
```

### Controller Integration Test

```java
@SpringBootTest
@AutoConfigureMockMvc
class UserControllerIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    @DisplayName("GET /api/users should return OK")
    void getUsers_ReturnsOk() throws Exception {
        mockMvc.perform(get("/api/users"))
            .andExpect(status().isOk())
            .andExpect(content().contentType(MediaType.APPLICATION_JSON));
    }

    @Test
    @DisplayName("GET /api/users/{id} with invalid ID should return 404")
    void getUser_WithInvalidId_ReturnsNotFound() throws Exception {
        mockMvc.perform(get("/api/users/99999"))
            .andExpect(status().isNotFound());
    }

    @Test
    @DisplayName("POST /api/users with valid data should return 201")
    void createUser_WithValidData_ReturnsCreated() throws Exception {
        CreateUserDto dto = new CreateUserDto("Jane Doe", "jane@example.com");

        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(dto)))
            .andExpect(status().isCreated())
            .andExpect(header().exists("Location"));
    }
}
```
