package xiaozhi.modules.model.service.impl;

import java.util.List;

import org.apache.commons.lang3.StringUtils;
import org.springframework.stereotype.Service;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;

import lombok.AllArgsConstructor;
import xiaozhi.common.service.impl.BaseServiceImpl;
import xiaozhi.common.utils.ConvertUtils;
import xiaozhi.modules.model.dao.ModelProviderDao;
import xiaozhi.modules.model.dto.ModelProviderDTO;
import xiaozhi.modules.model.entity.ModelProviderEntity;
import xiaozhi.modules.model.service.ModelProviderService;

@Service
@AllArgsConstructor
public class ModelProviderServiceImpl extends BaseServiceImpl<ModelProviderDao, ModelProviderEntity>
        implements ModelProviderService {

    private final ModelProviderDao modelProviderDao;

    @Override
    public List<ModelProviderDTO> getListByModelType(String modelType) {

        QueryWrapper<ModelProviderEntity> queryWrapper = new QueryWrapper<>();
        queryWrapper.eq("model_type", StringUtils.isBlank(modelType) ? "" : modelType);
        List<ModelProviderEntity> providerEntities = modelProviderDao.selectList(queryWrapper);
        return ConvertUtils.sourceToTarget(providerEntities, ModelProviderDTO.class);
    }

    @Override
    public ModelProviderDTO add(ModelProviderEntity modelProviderEntity) {
        return null;
    }

    @Override
    public ModelProviderDTO edit(ModelProviderEntity modelProviderEntity) {
        return null;
    }

    @Override
    public void delete() {

    }

    @Override
    public List<ModelProviderDTO> getList(String modelType, String provideCode) {
        QueryWrapper<ModelProviderEntity> queryWrapper = new QueryWrapper<>();
        queryWrapper.eq("model_type", StringUtils.isBlank(modelType) ? "" : modelType);
        queryWrapper.eq("provide_code", StringUtils.isBlank(provideCode) ? "" : provideCode);
        List<ModelProviderEntity> providerEntities = modelProviderDao.selectList(queryWrapper);
        return ConvertUtils.sourceToTarget(providerEntities, ModelProviderDTO.class);
    }

    @Override
    public List<String> getFieldList(String modelType, String provideCode) {
        // TODO: 获取模型供应器字段
        return modelProviderDao.getFieldList(modelType, provideCode);
    }
}
