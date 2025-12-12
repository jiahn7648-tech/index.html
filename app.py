import streamlit as st
import streamlit.components.v1 as components
import base64

# 1. 페이지 설정
st.set_page_config(page_title="3D 큐브 텍스처 앱", layout="wide")

st.title("🖼️ 나만의 사진으로 3D 큐브 만들기")
st.write("이미지를 업로드하면 큐브의 표면이 바뀝니다!")

# 2. 파일 업로더 추가
uploaded_file = st.file_uploader("이미지 파일을 선택하세요 (jpg, png)", type=['png', 'jpg', 'jpeg'])

# 3. 이미지가 있으면 Base64 문자열로 변환, 없으면 null 처리
texture_data = "null"

if uploaded_file is not None:
    # 파일을 읽어서 바이트로 변환
    bytes_data = uploaded_file.getvalue()
    # 바이트를 base64 문자열로 인코딩
    base64_str = base64.b64encode(bytes_data).decode()
    # 자바스크립트에서 쓸 수 있는 포맷으로 가공
    mime_type = uploaded_file.type
    texture_data = f"'data:{mime_type};base64,{base64_str}'"

# 4. HTML/JS 코드 작성 (f-string을 사용하여 texture_data 변수를 주입)
# 주의: f-string 내부에서는 자바스크립트의 중괄호 {}를 {{}}로 두 번 써야 에러가 안 납니다.
cube_html = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <style>
        body {{ margin: 0; overflow: hidden; background-color: #0E1117; }}
        canvas {{ width: 100%; height: 100%; }}
    </style>
</head>
<body>
    <script type="importmap">
        {{
            "imports": {{
                "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
                "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
            }}
        }}
    </script>
    <script type="module">
        import * as THREE from 'three';
        import {{ OrbitControls }} from 'three/addons/controls/OrbitControls.js';

        // --- 파이썬에서 전달받은 이미지 데이터 ---
        const textureUrl = {texture_data}; 

        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0E1117);

        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.z = 4;

        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        const geometry = new THREE.BoxGeometry(1.5, 1.5, 1.5);
        
        // --- 텍스처 로직 변경 부분 ---
        let material;

        if (textureUrl) {{
            // 1. 이미지가 있으면: 텍스처 로더를 사용해 이미지를 입힘
            const loader = new THREE.TextureLoader();
            const texture = loader.load(textureUrl);
            // 색상 왜곡 방지를 위해 색 공간 설정 (선택사항)
            texture.colorSpace = THREE.SRGBColorSpace; 
            
            // MeshBasicMaterial은 빛이 없어도 이미지가 선명하게 보임
            material = new THREE.MeshBasicMaterial({{ map: texture }});
        }} else {{
            // 2. 이미지가 없으면: 기존의 알록달록한 재질 사용
            material = new THREE.MeshNormalMaterial();
        }}

        const cube = new THREE.Mesh(geometry, material);
        scene.add(cube);

        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;

        function animate() {{
            requestAnimationFrame(animate);
            cube.rotation.x += 0.005;
            cube.rotation.y += 0.005;
            controls.update();
            renderer.render(scene, camera);
        }}
        
        window.addEventListener('resize', function() {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }});

        animate();
    </script>
</body>
</html>
"""

# 5. 스트림릿 화면에 렌더링
components.html(cube_html, height=600)
